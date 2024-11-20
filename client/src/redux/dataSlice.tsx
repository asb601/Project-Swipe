import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface DataState {
  customers: any[];
  invoices: any[];
  products: any[];
  totals: any[];
  activeTab: string;
}

const initialState: DataState = {
  customers: [],
  invoices: [],
  products: [],
  totals: [],
  activeTab: "invoices",
};

export const dataSlice = createSlice({
  name: "data",
  initialState,
  reducers: {
    setData(state, action: PayloadAction<any>) {
      // Map backend keys to Redux state keys
      const { Customers, Invoices, Products, Totals } = action.payload;

      state.customers = Customers || [];
      state.invoices = Invoices || [];
      state.products = Products || [];
      state.totals = Totals || [];
    },
    setActiveTab(state, action: PayloadAction<string>) {
      state.activeTab = action.payload;
    },
  },
});

export const { setData, setActiveTab } = dataSlice.actions;

export default dataSlice.reducer;
