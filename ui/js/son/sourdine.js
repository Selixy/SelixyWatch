let forcee = false;

export const estForcee = () => forcee;

export function sourdineForcee(b) {
  forcee = b;
  window.dispatchEvent(new Event('son-local'));
}
