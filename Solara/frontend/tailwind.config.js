/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        solara: {
          bg: '#fdfaf2',      // Warm cream background
          accent: '#f97316',  // Solar orange
          yellow: '#fcd34d',  // Sun yellow
          card: '#ffffff',    // Pure white cards
          text: '#452e1a',    // Dark chocolate text (softer than black)
          green: '#22c55e',
          red: '#ef4444'
        }
      },
      backgroundImage: {
        'dotted-pattern': "radial-gradient(#e5e7eb 1px, transparent 1px)",
      }
    },
  },
  plugins: [],
}








// /** @type {import('tailwindcss').Config} */
// export default {
//   content: [
//     "./index.html",
//     "./src/**/*.{js,ts,jsx,tsx}",
//   ],
//   theme: {
//     extend: {
//       colors: {
//         solara: {
//           dark: '#060b18',
//           orange: '#f97316',
//         }
//       },
//       borderRadius: {
//         '4xl': '2.5rem',
//       }
//     },
//   },
//   plugins: [],
// }