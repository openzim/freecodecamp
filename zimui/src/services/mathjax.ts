/*
Service to handle DOM manipulation to add/remove MathJax everytime needed.

This is a bit hackhish to remove and and back MathJax, but it is the only reliable
solution found so far, and probably the most robust one.

The dynamic behavior of removing / adding back MathJax is wanted/necessary because we
need to dynamically set the PageIndex macro to dynamically display proper figures
/ equations / ... numbering.

MathJax settings are an adaptation of libretexts.org settings, for MathJax 3 (including
extensions now removed or not yet supported or included by default).
*/

class MathJaxService {
  removeMathJax() {
    const script = document.getElementById('mathjax-script')
    if (script) script.remove()
    if (window.MathJax) delete window.MathJax
  }

  addMathJax() {
    window.MathJax = {
      tex: {
        inlineMath: [
          ['$', '$'],
          ['\\(', '\\)']
        ],
        processEscapes: true
      }
    }
    const script = document.createElement('script', {
      id: 'mathjax-script'
    } as ElementCreationOptions)
    script.src = './mathjax/es5/tex-svg.js'
    document.head.appendChild(script)
  }
}

const mathjaxService = new MathJaxService()
Object.freeze(mathjaxService)

export default mathjaxService
