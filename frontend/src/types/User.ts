export interface User {
    id: string;
    username: string;
    email: string;
    role: string;
    first_name: string;
    last_name: string;
    is_active: boolean;
    created_at: string;
    deleted_at: string | null;
}

