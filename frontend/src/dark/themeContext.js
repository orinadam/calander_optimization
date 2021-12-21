import { createContext } from "react";

export const themes = {
  dark: "black-content",
  light: "white-content",
};

export const ThemeContext = createContext({
    theme: themes.dark,
  changeTheme: () => {},
});