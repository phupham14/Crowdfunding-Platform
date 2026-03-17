export interface Transaction {
  id: number;
  type: 'INVEST' | 'FUND_IN' | 'WITHDRAW' | 'RETURN';
  amount: number;
  projectName?: string; // chỉ dùng cho INVEST
  date: string;
  status: 'Pending' | 'Completed' | 'Failed';
}
