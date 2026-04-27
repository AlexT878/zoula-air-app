import { UI_TEXT } from "./text";

export const MAX_PASSENGERS = 25;

const { terms: passengerTerms } = UI_TEXT.hero.inputs.passengers;
export const CATEGORIES = [
  {
    id: "adults",
    label: passengerTerms.adult_plural,
    sub: passengerTerms.years16,
  },
  {
    id: "youngAdults",
    label: passengerTerms.young_adults,
    sub: passengerTerms.years12,
  },
  {
    id: "children",
    label: passengerTerms.children,
    sub: passengerTerms.years11,
  },
  {
    id: "infants",
    label: passengerTerms.infant,
    sub: passengerTerms.years_infant,
  },
];
