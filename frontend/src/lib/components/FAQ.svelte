<script lang="ts">
	import {
		Accordion,
		AccordionContent,
		AccordionItem,
		AccordionTrigger
	} from '$lib/components/ui/accordion';

	const faqs = [
		{
			question: 'What are access controls?',
			answer:
				'Access controls allow you to manage who can view or download your images. You can set permissions for specific users or groups, ensuring that only authorized individuals have access to your content.'
		},
		{
			question: 'Are there any costs associated with these features?',
			answer:
				'Our image protection features come at no additional cost. We believe in empowering users to safeguard their content without financial barriers, making it accessible for everyone.'
		},
		{
			question: 'Is it possible to add metadata to my images?',
			answer:
				'Yes, you can embed metadata directly into your images. This includes details like ownership, copyright information, and usage rights, which can be crucial for legal protection and attribution.'
		}
	];
</script>

<section class="w-full px-4 md:px-6">
	<div class="mx-auto max-w-3xl">
		<h2 class="mb-4 text-center text-3xl font-bold tracking-tighter">Protect Your Images</h2>
		<p class="mb-8 text-center text-muted-foreground">Secure Your Visual Content</p>

		<Accordion type="single" collapsible>
			{#each faqs as faq, i}
				<AccordionItem value="item-{i}">
					<AccordionTrigger>{faq.question}</AccordionTrigger>
					<AccordionContent>
						{faq.answer}
					</AccordionContent>
				</AccordionItem>
			{/each}
		</Accordion>
	</div>
</section>
