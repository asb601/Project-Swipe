import {
  Table,
  TableBody,
  TableCaption,
  TableHead,
  TableHeader,
  TableRow,
  TableCell,
} from "@/components/ui/table";
import { useSelector } from "react-redux";
import { RootState } from "../redux/store";

export const CustomersTable = ({ onTabChange }: { onTabChange: (tab: string) => void }) => {
  const customers = useSelector((state: RootState) => state.data.customers);


  console.log("Customers Data in CustomersTable:", customers);

  if (!customers || customers.length === 0) {
    console.warn("No Customers Found. Customers Data:", customers);
    return <div className="text-center m-3">No Customers Found</div>;
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-center text-2xl font-semibold text-gray-800 mb-6">
        Customers
      </h2>
      <Table className="w-full border border-gray-200 rounded-lg overflow-hidden">
        <TableCaption className="text-gray-500 text-sm">
          A list of recent customers
        </TableCaption>
        <TableHeader className="bg-gray-100">
          <TableRow>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Customer Name
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Phone Number
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Total Purchase Amount
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {customers.map((customer: any, index: any) => (
            <TableRow
              key={index}
              className={`${
                index % 2 === 0 ? "bg-gray-50" : "bg-white"
              } hover:bg-gray-100 transition-colors`}
            >
              <TableCell className="px-4 py-2 text-gray-800">
                {customer.customerName}
              </TableCell>
              <TableCell className="px-4 py-2 text-gray-800">
                {customer.phoneNumber}
              </TableCell>
              <TableCell className="px-4 py-2 text-gray-800">
                ₹{customer.totalPurchaseAmount}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
  
};
