// Vérifie que la sortie du moteur (objet Carte) est acceptée par MatheuxBilanPDF.render (js/bilan-pdf.js).
// Lancer après moteur_test.ts (qui écrit les fixtures) :
//   deno test --allow-read --allow-net supabase/tests/carte_pdf_test.ts
// deno-lint-ignore-file no-explicit-any
const ICI = new URL(".", import.meta.url);
const RACINE = new URL("../../", ICI);

Deno.test("carte moteur → PDF (complet + aperçu express)", async () => {
  const { jsPDF } = await import("npm:jspdf@2.5.2");
  const g: any = globalThis;
  g.jspdf = { jsPDF };
  (0, eval)(await Deno.readTextFile(new URL("js/bilan-pdf.js", RACINE)));
  const loadAsset = async (f: string) => {
    const b = await Deno.readFile(new URL("js/bilan-pdf-assets/" + f, RACINE));
    let s = ""; for (const x of b) s += String.fromCharCode(x);
    return btoa(s);
  };
  for (const [fichier, apercu] of [["carte_exemple_complet.json", false], ["carte_exemple_express.json", true]] as const) {
    const carte = JSON.parse(await Deno.readTextFile(new URL("fixtures/" + fichier, ICI)));
    const r = await g.MatheuxBilanPDF.render(carte, { apercu, loadAsset, cta: { label: "Débloquer", prix: "19 €" } });
    console.log(`  ${fichier} → ${r.fileName} · ${r.pageCount} pages · polices ${r.fontsEmbedded ? "intégrées" : "fallback"} · ${Math.round(r.blob.size / 1024)} Ko`);
    if (r.pageCount < (apercu ? 3 : 6)) throw new Error("PDF trop court : " + r.pageCount + " pages");
  }
});
