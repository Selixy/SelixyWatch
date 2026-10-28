const SONDE_STYLE = 'position:fixed;visibility:hidden;pointer-events:none;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)';
let sonde = null;

export function mesurerZones() {
  const s = getComputedStyle(sonde);
  const v = { '--sa-t': s.paddingTop, '--sa-r': s.paddingRight, '--sa-b': s.paddingBottom, '--sa-l': s.paddingLeft };
  const cadres = [...document.querySelectorAll('iframe[data-vue]')].map((f) => f.contentDocument?.documentElement);
  for (const d of [document.documentElement, ...cadres]) {
    if (d) for (const [k, x] of Object.entries(v)) d.style.setProperty(k, x);
  }
}

export function brancherZones() {
  sonde = document.createElement('div');
  sonde.style.cssText = SONDE_STYLE;
  document.body.append(sonde);
  for (const f of document.querySelectorAll('iframe[data-vue]')) f.addEventListener('load', mesurerZones);
  addEventListener('resize', mesurerZones);
  addEventListener('orientationchange', mesurerZones);
}
