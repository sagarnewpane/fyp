import { z } from 'zod';

export const profileSchema = z.object({
	username: z
		.string()
		.min(3, 'Username must be at least 3 characters')
		.max(50, 'Username must be less than 50 characters'),
	first_name: z
		.string()
		.min(2, 'First name must be at least 2 characters')
		.max(50, 'First name must be less than 50 characters'),
	last_name: z
		.string()
		.min(2, 'Last name must be at least 2 characters')
		.max(50, 'Last name must be less than 50 characters'),
	email: z.string().email('Invalid email address'),
	social_links: z.object({
		website: z.string().url('Invalid website URL').optional().or(z.literal('')),
		twitter: z
			.string()
			.regex(/^@?(\w){1,15}$/, 'Invalid Twitter username')
			.optional()
			.or(z.literal('')),
		instagram: z
			.string()
			.regex(/^@?(\w){1,30}$/, 'Invalid Instagram username')
			.optional()
			.or(z.literal(''))
	})
});

export const avatarSchema = z.object({
	file: z
		.instanceof(File)
		.refine((file) => file.size <= 5 * 1024 * 1024, 'File size must be less than 5MB')
		.refine(
			(file) => ['image/jpeg', 'image/png', 'image/gif'].includes(file.type),
			'Only .jpg, .png, and .gif files are allowed'
		)
});

export const passwordChangeSchema = z
	.object({
		current_password: z.string().min(1, 'Current password is required'),
		new_password: z
			.string()
			.min(8, 'Password must be at least 8 characters')
			.regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
			.regex(/[a-z]/, 'Password must contain at least one lowercase letter')
			.regex(/[0-9]/, 'Password must contain at least one number'),
		confirm_password: z.string().min(1, 'Please confirm your password')
	})
	.refine((data) => data.new_password === data.confirm_password, {
		message: "Passwords don't match",
		path: ['confirm_password']
	});
