import { z } from 'zod';

export const emailSchema = z.string().email('Invalid email address');

export const protectionFeaturesSchema = z.object({
	watermark: z.boolean().optional().default(false),
	hidden_watermark: z.boolean().optional().default(false),
	metadata: z.boolean().optional().default(false),
	ai_protection: z.boolean().optional().default(false)
});

export const accessControlSchema = z.object({
	access_name: z
		.string()
		.min(1, 'Access name is required')
		.max(50, 'Access name must be less than 50 characters'),
	allowed_emails: z.array(emailSchema).optional().default([]),
	requires_password: z.boolean().optional().default(false),
	password: z.string().superRefine((val, ctx) => {
		if (ctx.parent.requires_password && (!val || val.length < 6)) {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Password must be at least 6 characters when password protection is enabled'
			});
		}
	}),
	allow_download: z.boolean().optional().default(false),
	max_views: z
		.number()
		.int('Must be a whole number')
		.min(0, 'Cannot be negative')
		.optional()
		.default(0),
	protection_features: protectionFeaturesSchema.optional().default({
		watermark: false,
		hidden_watermark: false,
		metadata: false,
		ai_protection: false
	})
});
