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
