Usage: fcc2zim_poc

Suposes that I've built fcc UI in /home/benoit/Repos/freeCodeCamp/freeCodeCamp/dist


# Problems encountered and "hacked"

- bug in rewrite of import statements: it rewrite also import statement in strings ... and break the string ...
  - hacked by manually back-rewriting these (with .replace(..., ...))
- bug in _____WB$wombat$check$this$function_____ which is undefined
  - did not understood it so far, just back-rewriting this as well (with .replace(..., ...))
- load wombat inside fcc-test-frame
  - manual hack of dist/www.freecodecamp.org/app-dae57cd12b32d17253ca.js to load wombat (specifically for the www.freecodecamp.org/learn/data-visualization/data-visualization-with-d3/work-with-data-in-d3 page, generalization not done but probably feasible)
- properly rewrite HTML of fcc-test-frame
  - only rewrite URL of /js/frame-runner-f60ef84037d469dc5ee4.js to ../../../js/frame-runner-f60ef84037d469dc5ee4.js, done manually in dist/www.freecodecamp.org/app-dae57cd12b32d17253ca.js as well (with `<script id="fcc-test-runner" src=\'../../..'+o+"'`)
- donation modal always showing up
  - hacked in dist/www.freecodecamp.org/app-dae57cd12b32d17253ca.js as well with `if(false&&(e||r)){yield(0,u.cb)(200)`

# Problems encountered and not solved

- for pages to work, sometimes you need to add a trailing slash, something you need to remove it
  - home needs to be www.freecodecamp.org/
  - learn needs to be www.freecodecamp.org/learn/
  - data-visualization module needs to be www.freecodecamp.org/learn/data-visualization/
  - course needs to be www.freecodecamp.org/learn/data-visualization/data-visualization-with-d3/work-with-data-in-d3
  - probably easily solvable, just didn't spent time on this

Bigger concern:
- error message "SyntaxError: invalid range in character class" in UI Console (not JS console) after loading the page
- error message "[TypeError: $(...).text().match(...) is null]" in UI Console (not JS console) after running the tests
- error message "TypeError: Oi.transform is not a function"  in UI Console (not JS console) after typing some code in the UI

Something on this bigger concern (or something else) prevent the UI from fully functionning on course tests
