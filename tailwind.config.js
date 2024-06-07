/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './Blog/templates/**/*.html',
    './authentication/templates/**/*.html',
    './static_files/css/**/*.css',
  ],
  theme: {
    extend: {
      textDecoration: ['responsive', 'hover', 'focus', 'focus-visible', 'active'],
      fontWeight: ['responsive', 'hover', 'focus', 'focus-visible', 'active'],
      fontFamily: {
        'sans': ['Open Sans', 'ui-sans-serif', 'system-ui'],
        'serif': ['Merriweather', 'ui-serif', 'Georgia'],
        'mono': ['Source Code Pro', 'ui-monospace', 'monospace'],
      },
      height: {
        '70': '70px',
        '35': '35px',
      },
      width: {
        '20p': '20%',
        '40p': '40%',
        '60p': '60%',
        '70p': '70%',
        '80p': '80%',
        '90p': '90%',
        '100p': '100%',
      },
      padding: {
        '1p': '1%',
        '4p': '4%',
      },
      margin: {
        '5p': '5%',
        
      },
    },
  },
  variants: {
    extend: {
      textDecoration: ['responsive', 'hover', 'focus', 'active'],
      fontWeight: ['responsive', 'hover', 'focus', 'active'],
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/line-clamp'),
  ],
}