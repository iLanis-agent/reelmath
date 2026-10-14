// Reel math - fishing reel and line honesty.
// The yardage sticker assumed one diameter of mono. Braid lies by diameter,
// the rod's casting window is a loading range, and the quarter-ounce drawer
// belongs to a lake at dawn.
// Verdicts judge the unrounded figure; rounding is for display only.
var ReelMath = (function () {
  function pos(x) { return typeof x === "number" && isFinite(x) && x > 0; }
  function num(x) { return typeof x === "number" && isFinite(x); }
  function r1(x) { return Math.round(x * 10) / 10; }

  // Labeled norms: diameter in mm by line test.
  var MONO = { "6": 0.23, "8": 0.25, "10": 0.28, "12": 0.31, "14": 0.33, "17": 0.36, "20": 0.41 };
  var BRAID = { "8": 0.13, "10": 0.15, "15": 0.19, "20": 0.23, "30": 0.28, "40": 0.32, "50": 0.36 };
  var FLUORO = { "8": 0.26, "10": 0.29, "12": 0.32, "15": 0.35, "20": 0.41 };
  var TABLES = { mono: MONO, braid: BRAID, fluoro: FLUORO };

  function capacityPlan(spoolYd, spoolLb, lineType, lineLb) {
    if (!pos(spoolYd)) return { error: "the spool yardage must be above zero" };
    if (!MONO[spoolLb]) return { error: "pick the sticker's line test" };
    if (!TABLES[lineType]) return { error: "pick a line type" };
    if (!TABLES[lineType][lineLb]) return { error: "pick your line's test" };
    // A spool holds cross-section area times length: capacity scales with the
    // square of the diameter ratio.
    var yd = spoolYd * Math.pow(MONO[spoolLb] / TABLES[lineType][lineLb], 2);
    return { yd: r1(yd) };
  }

  function renderCapacity(r, spoolYd, spoolLb, lineType, lineLb) {
    return "Your " + spoolYd + " yd / " + spoolLb + " lb spool holds about " + r.yd + " yds of " + lineLb
      + " lb " + lineType + " - the sticker line was mono, and the spool never read the box.";
  }

  function windowPlan(lureOz, rodMin, rodMax) {
    if (!pos(lureOz) || !pos(rodMin) || !pos(rodMax)) return { error: "ounces must all be above zero" };
    if (rodMin >= rodMax) return { error: "the window's low end must sit under its high end" };
    var verdict = lureOz < rodMin ? "under" : lureOz > rodMax ? "over" : "inside";
    return { verdict: verdict };
  }

  function renderWindow(r, lureOz, rodMin, rodMax) {
    if (r.verdict === "inside") {
      return "Your " + lureOz + " oz lure sits inside the rod's " + rodMin + "-" + rodMax
        + " oz window - the blank loads the way the sticker promised.";
    }
    if (r.verdict === "under") {
      return "Your " + lureOz + " oz lure never reaches the " + rodMin + " oz bottom of the rod's window - the blank barely bends, and the cast dies early.";
    }
    return "Your " + lureOz + " oz lure is past the " + rodMax + " oz top of the rod's window - the blank folds instead of loading, and the cast dies early.";
  }

  function sinkerPlan(depthFt, currentMph) {
    if (!pos(depthFt)) return { error: "the depth must be above zero" };
    if (!num(currentMph) || currentMph < 0) return { error: "the current must be zero or more" };
    // Labeled norm: an ounce per ten feet of depth per mph of current.
    var oz = depthFt * currentMph / 10;
    if (oz <= 0) oz = 0.25;
    return { oz: r1(oz) };
  }

  function renderSinker(r, depthFt, currentMph) {
    return "Your " + depthFt + " ft at " + currentMph + " mph figures about " + r.oz
      + " oz of lead - the quarter-ounce drawer belongs to a lake at dawn.";
  }

  return {
    capacityPlan: capacityPlan, renderCapacity: renderCapacity,
    windowPlan: windowPlan, renderWindow: renderWindow,
    sinkerPlan: sinkerPlan, renderSinker: renderSinker
  };
})();
if (typeof module !== "undefined") module.exports = ReelMath;
