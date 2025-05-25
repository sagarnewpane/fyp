import { z } from 'zod';

export const formSchema = z
	.object({
		new_password: z
			.string()
			.min(8, 'Password must be at least 8 characters')
			.regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
			.regex(/[a-z]/, 'Password must contain at least one lowercase letter')
			.regex(/[0-9]/, 'Password must contain at least one number')
			.regex(/[!@#$%^&*(),.?":{}|<>]/, 'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)'),
		confirm_password: z.string()
	})
	.refine((data) => data.new_password === data.confirm_password, {
		message: "Passwords don't match",
		path: ['confirm_password']
	});
