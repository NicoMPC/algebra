// Test de non-régression de la comparaison des réponses fill (app.html).
// Usage : node supabase/tests/fill_match_node.js  (depuis la racine du repo)
const fs=require('fs');const src=fs.readFileSync('app.html','utf8');
const a=src.indexOf('function _normFill'),b=src.indexOf('// ─── SÉLECTION + VALIDATION QCM');
eval(src.slice(a,b));
const T=[["+15","15",true],["x=−7","-7",true],["−5","-5",true],["x=4","4",true],["a=3","3",true],["y=2x+3","y=2x+3",true],["x=5","4",false],
["4x+3","4x+12",false],["8×10^5","8×10^-5",false],["4x+12","4x+12",true],["0,7","7/10",true],["70%","0.7",true],
["-3","-3",true],["2.50","2,5",true],[" 12 ","12",true],["12cm","12",true],["12 cm²","12",true],["12x","12",false],["3a","3",false],[".5","0,5",true]];
let ok=true;for(const [u,c,exp] of T){const r=_matchFill(u,c,[]);if(r!==exp){ok=false;console.log("FAIL",u,c,r)}}console.log(ok?"all ok":"failures");
if(!ok)process.exit(1);
