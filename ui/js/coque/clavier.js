export function suivreClavier() {
  const vv = window.visualViewport;
  if (!vv) return;
  const racine = document.documentElement;
  const suivre = () => {
    if (vv.scale > 1.01) return;
    racine.style.setProperty('--hauteur', `${Math.round(vv.height)}px`);
    racine.style.setProperty('--decalage', `${Math.round(vv.offsetTop)}px`);
    racine.classList.toggle('decale', vv.offsetTop > 0);
  };
  vv.addEventListener('resize', suivre);
  vv.addEventListener('scroll', suivre);
  suivre();
}
