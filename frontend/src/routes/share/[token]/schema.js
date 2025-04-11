import { z } from 'zod';

export const emailSchema = z.object({
	email: z.string().min(1, 'Email is required').email('Please enter a valid email address')
});

export const passwordSchema = z.object({
	password: z.string().min(1, 'Password is required')
});

export const otpSchema = z.object({
	otp: z
		.string()
		.min(4, 'Verification code must be at least 4 characters')
		.max(6, 'Verification code cannot exceed 6 characters')
		.regex(/^\d+$/, 'Verification code must contain only numbers')
});

export const accessRequestSchema = z.object({
	email: z.string().min(1, 'Email is required').email('Please enter a valid email address'),
	message: z
		.string()
		.max(500, 'Message cannot exceed 500 characters')
		.optional()
		.transform((val) => val || '')
});
