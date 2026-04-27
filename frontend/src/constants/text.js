export const UI_TEXT = {
  header: {
    nav: [
      { name: "Home", path: "/" },
      { name: "Flights", path: "/flights" },
      { name: "Destinations", path: "/destinations" },
      { name: "Deals", path: "/deals" },
      { name: "Contact", path: "/contact" },
    ],
    signIn: "Sign In",
    logo: "Zoula Air",
  },

  hero: {
    title: "Your Journey Begins Here",
    subTitle: "Discover the world with comfort and style",
    options: [
      { value: "round-trip", text: "Round Trip" },
      { value: "one-way", text: "One Way" },
      { value: "multi-city", text: "Multi City" },
    ],
    inputs: {
      from: {
        label: "From",
        placeholder: "New York (JFK)",
      },
      to: {
        label: "To",
        placeholder: "London (LHR)",
      },
      departure: {
        label: "Departure",
        placeholder: "Departure",
      },
      return: {
        placeholder: "Return",
      },
      passengers: {
        label: "Passengers",
        terms: {
          adult_singular: "Adult",
          adult_plural: "Adults",
          other_singular: "Other",
          other_plural: "Others",
          young_adults: "Young adults",
          children: "Children",
          infant: "Infants",
          years16: "16+ years",
          years12: "12-15 years",
          years11: "2-11 years",
          years_infant: "Under 2 years",
        },
      },
      submit: "Search Flights",
    },
  },

  modal: {
    got_it: "Got it",
    infant: {
      title: "Infant Seating Policy",
      text: "Infants (under 2 years) must sit on an adult’s lap. The infant will automatically be linked to the first adult (aged 18+) on the booking.",
    },
  },

  alerts: {
    maximum_passangers:
      "The maximum number of passengers is 25. If there are more than 25 passengers please use our group booking form.",
    no_departure_city: "Enter a departure city.",
    max_departure_city: "Departure location must be at most 32 characters.",
    no_arrival_city: "Enter an arrival city.",
    max_arrival_city: "Arrival location must be at most 32 characters.",
    no_date: "Select a date.",
    no_passangers: "Required.",
  },
};
