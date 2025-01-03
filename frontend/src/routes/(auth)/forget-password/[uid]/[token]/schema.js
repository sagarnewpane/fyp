import { z } from 'zod';

export const formSchema = z
	.object({
		new_password: z.string().min(8, 'Password must be at least 8 characters'),
		confirm_password: z.string()
	})
	.refine((data) => data.new_password === data.confirm_password, {
		message: "Passwords don't match",
		path: ['confirm_password']
	});
