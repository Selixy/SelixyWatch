export const retourner = () => (window.top !== window ? parent.postMessage({ type: 'recharger', vue: 'room' }, location.origin) : (location.href = '/#room'));

export const prevenirCoque = () => { if (window.top !== window) parent.postMessage({ type: 'compte' }, location.origin); };
