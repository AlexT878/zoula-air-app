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
        placeholder: "1 Adult",
      },
      submit: "Search Flights",
    },
  },
};
