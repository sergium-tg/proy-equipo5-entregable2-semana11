
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        coffee: {
          50:"#f3ece8",100:"#e9ddd6",200:"#d9c4b7",300:"#c8aa98",
          400:"#b88f78",500:"#8a5e4d",600:"#6b4a3c",700:"#513a2f",
          800:"#3a2a23",900:"#2a1e19",950:"#1e1612"
        },
        cream: { 50:"#fbf7f3",100:"#f8f4f0",200:"#efe3d8" },
        pearl: { 50:"#f8f7f6" },
      },
      boxShadow: { soft: "0 8px 30px rgba(0,0,0,0.08)" },
      borderRadius: { "2xl": "1.25rem" }
    },
  },
  plugins: [],
}
