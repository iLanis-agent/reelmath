# Reel Math

The fishing line honesty tool. The yardage sticker assumed one diameter
of mono. Reel Math converts a spool's sticker to your actual line by the
square of the diameter ratio, checks your lure against the rod's loading
window, and budgets lead for real current.

- Live app: https://ilanis-agent.github.io/reelmath/app.html
- Landing: https://ilanis-agent.github.io/reelmath/

## What it does

1. **The spool truth** - capacity scales with the square of the diameter
   ratio against the sticker's mono (labeled diameter norms for mono,
   braid and fluoro).
2. **The casting window** - lure weight against the rod's printed
   loading range; under it the blank barely bends, past it the blank folds.
3. **The lead budget** - an ounce per ten feet of depth per mph of
   current, with a quarter-ounce floor.

## Files

- `engine.js` - pure functions (`capacityPlan`, `windowPlan`, `sinkerPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 29 oracle cases, `node test.js` runs green

The tables are labeled norms; the river keeps its own ledger.
