export function regrouper(action, delai = 120, planifier = setTimeout) {
  let planifie = false;
  let enCours = false;
  let redemande = false;

  async function lancer() {
    planifie = false;
    enCours = true;
    try { await action(); } finally { enCours = false; }
    if (redemande) { redemande = false; demander(); }
  }

  function demander() {
    if (enCours) { redemande = true; return; }
    if (planifie) return;
    planifie = true;
    planifier(lancer, delai);
  }

  return demander;
}
