export type Complaint = {
  id: number;
  reference_number: string | null;
  complaint_type: string | null;
  main_category: string | null;
  fraud_type: string | null;
  sub_type: string | null;
  status: string;
  name: string | null;
  phone_number: string | null;
  email_id: string | null;
  district: string | null;
  created_at: string;
  updated_at: string | null;
  documents: string | string[] | null;
  user: { wa_id: string };
  data?: string;
};

