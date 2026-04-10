"""
supabase_helper.py — Wrapper Supabase REST pour les scripts Python Matheux.
Remplace l'ancien sheets.py (Google Sheets API) supprimé le 02/04/2026.

Usage:
    from supabase_helper import sb
    profiles = sb.read('profiles')
    sb.insert('scores', [{'code': 'TEST01', 'chapitre': 'Fractions', ...}])
    sb.update('profiles', {'code': 'eq.TEST01'}, {'niveau': '3EME'})
    sb.delete('scores', {'code': 'eq.TEST01'})
"""

import os, json, requests
from datetime import date

# --- Config ---
_SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://xlfzhcanzmqqlxtavzrd.supabase.co')
_SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Fallback: lire depuis .env si pas dans l'environnement
if not _SUPABASE_KEY:
    _env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    _env_supa = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env.supabase')
    for p in [_env_path, _env_supa]:
        if os.path.exists(p):
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('SUPABASE_SERVICE_ROLE_KEY='):
                        _SUPABASE_KEY = line.split('=', 1)[1]
                    elif line.startswith('SUPABASE_URL='):
                        _SUPABASE_URL = line.split('=', 1)[1]


# --- API Matheux (Edge Function) ---
API_URL = f'{_SUPABASE_URL}/functions/v1/api'

def api_call(action, **kwargs):
    """Appel à l'Edge Function api. Retourne le JSON de réponse."""
    payload = {'action': action, **kwargs}
    r = requests.post(API_URL, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


# --- Supabase REST ---
class SupabaseHelper:
    """Client REST Supabase avec service_role key (bypass RLS)."""

    def __init__(self):
        if not _SUPABASE_KEY:
            raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY manquant. Vérifier .env ou .env.supabase")
        self.base = f'{_SUPABASE_URL}/rest/v1'
        self._headers = {
            'apikey': _SUPABASE_KEY,
            'Authorization': f'Bearer {_SUPABASE_KEY}',
            'Content-Type': 'application/json',
        }

    def _h(self, extra=None):
        h = dict(self._headers)
        if extra:
            h.update(extra)
        return h

    # ── Read ──────────────────────────────────────────────

    def read(self, table, select='*', filters=None, order=None, limit=None):
        """
        Lire des lignes.
        filters: dict de filtres PostgREST, ex: {'code': 'eq.TEST01', 'is_test': 'eq.false'}
        order: str, ex: 'date.desc'
        Retourne list[dict].
        """
        params = {'select': select}
        if filters:
            params.update(filters)
        if order:
            params['order'] = order
        if limit:
            params['limit'] = str(limit)
        r = requests.get(f'{self.base}/{table}', headers=self._h(), params=params, timeout=15)
        r.raise_for_status()
        return r.json()

    def read_one(self, table, select='*', filters=None):
        """Lire une seule ligne (ou None)."""
        rows = self.read(table, select=select, filters=filters, limit=1)
        return rows[0] if rows else None

    def count(self, table, filters=None):
        """Compter les lignes."""
        h = self._h({'Prefer': 'count=exact', 'Range': '0-0'})
        params = {'select': 'id'}
        if filters:
            params.update(filters)
        r = requests.get(f'{self.base}/{table}', headers=h, params=params, timeout=15)
        r.raise_for_status()
        cr = r.headers.get('content-range', '*/0')
        total = cr.split('/')[-1]
        return int(total) if total != '*' else 0

    # ── Write ─────────────────────────────────────────────

    def insert(self, table, rows, upsert=False):
        """
        Insérer des lignes. rows = dict (1 ligne) ou list[dict].
        upsert=True → on-conflict merge.
        Retourne les lignes insérées.
        """
        if isinstance(rows, dict):
            rows = [rows]
        prefer = 'return=representation'
        if upsert:
            prefer += ',resolution=merge-duplicates'
        h = self._h({'Prefer': prefer})
        r = requests.post(f'{self.base}/{table}', headers=h, json=rows, timeout=15)
        r.raise_for_status()
        return r.json()

    def update(self, table, filters, data):
        """
        Update des lignes matchant les filtres.
        filters: dict PostgREST, ex: {'code': 'eq.TEST01'}
        data: dict des champs à modifier.
        """
        h = self._h({'Prefer': 'return=representation'})
        params = dict(filters)
        r = requests.patch(f'{self.base}/{table}', headers=h, params=params, json=data, timeout=15)
        r.raise_for_status()
        return r.json()

    def delete(self, table, filters):
        """
        Delete des lignes matchant les filtres.
        filters: dict PostgREST, ex: {'code': 'eq.TEST01'}
        """
        h = self._h({'Prefer': 'return=representation'})
        r = requests.delete(f'{self.base}/{table}', headers=h, params=filters, timeout=15)
        r.raise_for_status()
        return r.json()

    # ── Helpers métier ────────────────────────────────────

    def get_profiles(self, test=False, admin=False):
        """Profils réels (non-test, non-admin par défaut)."""
        f = {}
        if not test:
            f['is_test'] = 'eq.false'
        if not admin:
            f['is_admin'] = 'eq.false'
        return self.read('profiles', filters=f)

    def get_scores(self, code=None, source_neq=None):
        """Scores, optionnellement filtrés par code et/ou exclusion source."""
        f = {}
        if code:
            f['code'] = f'eq.{code}'
        if source_neq:
            f['source'] = f'neq.{source_neq}'
        return self.read('scores', filters=f)

    def get_boosts(self, code=None, date_val=None):
        """Daily boosts filtrés."""
        f = {}
        if code:
            f['code'] = f'eq.{code}'
        if date_val:
            f['date'] = f'eq.{date_val}'
        return self.read('daily_boosts', filters=f)

    def get_suivi(self, code=None):
        """Table suivi (admin dashboard)."""
        f = {}
        if code:
            f['code'] = f'eq.{code}'
        return self.read('suivi', filters=f)

    def get_curriculum(self, niveau=None, categorie=None):
        """Curriculum (exercices officiels)."""
        f = {}
        if niveau:
            f['niveau'] = f'eq.{niveau}'
        if categorie:
            f['categorie'] = f'eq.{categorie}'
        return self.read('curriculum', filters=f)

    def get_diagnostic_exos(self, niveau=None):
        """Exercices de diagnostic."""
        f = {}
        if niveau:
            f['niveau'] = f'eq.{niveau}'
        return self.read('diagnostic_exos', filters=f)

    def today(self):
        """Date du jour format YYYY-MM-DD."""
        return date.today().isoformat()


# Singleton
sb = SupabaseHelper()
