import { z } from 'zod';

export const formSchema = z.object({
	username: z.string().min(2).max(50),
	password: z.string().min(8).max(100)
});
