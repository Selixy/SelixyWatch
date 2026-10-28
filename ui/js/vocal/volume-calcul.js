export function calculerAudio({ individuel, muetIndividuel, maitre, muetMaitre }) {
  return {
    volume: Math.max(0, Math.min(1, individuel * maitre)),
    muet: muetIndividuel || muetMaitre,
  };
}
