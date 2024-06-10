/* eslint-disable semi */
// clash with TS default rules
export default interface UserCoordinates {
  dateTime: Date;
  lat: number;
  lng: number;
}

const degreeToRadian = (degree: number) => ((degree * Math.PI) / 180) as number;

// distância em coordenadas não é simplesmente distância em linha reta... É distância das cordas
// criada considerada a curvatura da terra
const haversineDistance = (
  coord1: UserCoordinates,
  coord2: UserCoordinates,
) => {
  const earthRadius = 6371000;

  const latRadianDistance = degreeToRadian(coord2.lat - coord1.lat);
  const lngRadianDistance = degreeToRadian(coord2.lng - coord1.lng);
  const halfChordSquared =
    Math.sin(latRadianDistance / 2) * Math.sin(latRadianDistance / 2) +
    Math.cos(degreeToRadian(coord1.lat)) *
    Math.cos(degreeToRadian(coord2.lat)) *
    Math.sin(lngRadianDistance / 2) * Math.sin(lngRadianDistance / 2);

  const angularDistance = 2 *
    Math.atan2(Math.sqrt(halfChordSquared), Math.sqrt(1 - halfChordSquared));
  const distance = earthRadius * angularDistance;

  return distance;
};

export const calculateTotalDistance = (coordinates: UserCoordinates[]) => {
  if (coordinates.length <= 1) {
    return 0;
  }

  let accumulatedDistance = 0;

  for (let i = 0; i < coordinates.length - 1; i += 1) {
    accumulatedDistance += haversineDistance(
      coordinates[i],
      coordinates[i + 1],
    );
  }

  return accumulatedDistance as number;
};
