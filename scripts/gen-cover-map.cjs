const fs = require("fs");
const dir = "public/images/blog/covers";
const files = fs.readdirSync(dir);
const map = {};
for (const file of files) {
  const slug = file.replace(/\.(jpg|jpeg|png|webp)$/i, "");
  if (slug !== file) {
    map[slug] = "/images/blog/covers/" + file;
  }
}
const output = "// Auto-generated — do not edit. Run: node scripts/gen-cover-map.js\nexport const coverImageMap: Record<string, string> = " + JSON.stringify(map, null, 2) + ";\n";
fs.writeFileSync("src/data/cover-map.ts", output);
console.log("Generated cover-map.ts with " + Object.keys(map).length + " entries");
