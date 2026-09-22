// dsh-session-errors.js — descomprime sesiones DSH (.zstd) y muestra errores de proveedor.
// Uso: node tools/dsh-session-errors.js <nSesionesRecientes>
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const base = 'C:\\Users\\USER\\.dsh\\sessions\\--C-Users-USER-Desktop--';
const n = Number(process.argv[2] || 4);

const dirs = fs.readdirSync(base, { withFileTypes: true })
  .filter(d => d.isDirectory())
  .map(d => ({ name: d.name, dir: path.join(base, d.name) }))
  .map(d => {
    const f = path.join(d.dir, 'session.v3.jsonl.zstd');
    return fs.existsSync(f) ? { ...d, file: f, mtime: fs.statSync(f).mtimeMs } : null;
  })
  .filter(Boolean)
  .sort((a, b) => b.mtime - a.mtime)
  .slice(0, n);

const PAT = /error|missing_credential|invalid_credential|rate.?limit|quota|unauthor|forbidden|failed|unknown_model|invalid_config|reject/i;

for (const d of dirs) {
  let text;
  try { text = zlib.zstdDecompressSync(fs.readFileSync(d.file)).toString('utf8'); }
  catch (e) { console.log(`\n=== ${d.name}: no se pudo descomprimir: ${e.message}`); continue; }

  const lines = text.split('\n').filter(Boolean);
  console.log(`\n================ ${d.name}  (${lines.length} registros) ================`);

  let hits = 0;
  for (const line of lines) {
    let j; try { j = JSON.parse(line); } catch { continue; }
    const s = JSON.stringify(j);
    const role = j.role || j.type || j.kind || '';
    const modelish = (j.model || j.provider || (j.message && j.message.model) || '');
    if (PAT.test(s) && (role || modelish)) {
      // recorta para no inundar
      console.log(`  [${role}] ${modelish ? 'model=' + modelish + ' ' : ''}${s.slice(0, 900)}`);
      if (++hits >= 6) { console.log('  ... (mas coincidencias omitidas)'); break; }
    }
  }
  if (!hits) console.log('  (sin lineas que coincidan con el patron de error)');
}
