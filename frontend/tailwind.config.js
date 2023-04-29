/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx}',
    './src/components/**/*.{js,ts,jsx,tsx}',
    './src/app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'dark-navy-blue': '#101727',
        'steel-blue': '#333b46',
      },
      fontFamily: {
        'varela-round': ['Varela Round', 'sans-serif']
      },
    },
  },
  plugins: [],
}
