export function sonAutorise() {
  const p = navigator.getAutoplayPolicy?.('mediaelement');
  if (p) return p === 'allowed';
  return navigator.userActivation ? navigator.userActivation.hasBeenActive : true;
}
