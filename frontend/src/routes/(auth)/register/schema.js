import { z } from 'zod';

export const formSchema = z
	.object({
		username: z.string().min(2).max(50),
		password1: z.string().min(8).max(100),
		password2: z.string().min(8).max(100),
		email: z.string().email().optional()
	})
	.refine((data) => data.password1 === data.password2, {
		message: "Passwords don't match",
		path: ['password2']
	});
