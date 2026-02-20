# Bring! MCP Server - Usage Examples

Practical examples of using the Bring! MCP Server with Claude Desktop.

## Basic Shopping List Operations

### Viewing Your Lists

```
You: Show me all my shopping lists

Claude: I'll get your shopping lists for you.

[Tool: bring_get_lists]

Shopping Lists:

Name: Weekly Groceries
UUID: abc123-def456-ghi789
Theme: cherry
---
Name: Party Shopping
UUID: xyz789-uvw456-rst123
Theme: watermelon
---
```

### Viewing List Items

```
You: What items are on my Weekly Groceries list?

Claude: Let me check what's on your Weekly Groceries list.

[Tool: bring_get_list_items]

Items in list abc123-def456-ghi789:

=== Active Items (To Purchase) ===
- Milk (low fat) [UUID: item-uuid-1]
- Eggs
- Bread (whole wheat) [UUID: item-uuid-2]
- Apples

=== Recently Completed ===
- Orange juice
- Cheese
```

## Adding Items

### Single Item

```
You: Add bananas to my Weekly Groceries list

Claude: I'll add bananas to your list.

[Tool: bring_add_item]
- list_uuid: abc123-def456-ghi789
- item_name: Bananas

Successfully added 'Bananas' to list abc123-def456-ghi789
```

### Item with Specification

```
You: Add organic honey to my Weekly Groceries

Claude: I'll add organic honey to your list.

[Tool: bring_add_item]
- list_uuid: abc123-def456-ghi789
- item_name: Honey
- specification: organic

Successfully added 'Honey (organic)' to list abc123-def456-ghi789
```

### Multiple Items at Once

```
You: Add these items to my list: tomatoes, lettuce, cucumbers, and carrots

Claude: I'll add all those items to your Weekly Groceries list.

[Tool: bring_batch_update_items]
- list_uuid: abc123-def456-ghi789
- operation: ADD
- items: 
  * Tomatoes
  * Lettuce
  * Cucumbers
  * Carrots

Successfully performed ADD operation on 4 item(s) in list abc123-def456-ghi789
```

### Multiple Items with Specifications

```
You: Add 2kg of potatoes, 1 liter of olive oil, and 500g of ground beef to my list

Claude: I'll add those items with their quantities.

[Tool: bring_batch_update_items]
- list_uuid: abc123-def456-ghi789
- operation: ADD
- items:
  * Potatoes (2kg)
  * Olive oil (1 liter)
  * Ground beef (500g)

Successfully performed ADD operation on 3 item(s)
```

## Completing Items

### Complete Single Item

```
You: Mark milk as purchased on my Weekly Groceries list

Claude: I'll mark milk as completed.

[Tool: bring_complete_item]
- list_uuid: abc123-def456-ghi789
- item_name: Milk

Successfully marked 'Milk' as completed in list abc123-def456-ghi789
```

### Complete Multiple Items

```
You: Mark eggs, bread, and apples as purchased

Claude: I'll mark those items as completed.

[Tool: bring_batch_update_items]
- operation: COMPLETE
- items: Eggs, Bread, Apples

Successfully performed COMPLETE operation on 3 item(s)
```

## Removing Items

### Remove Single Item

```
You: Remove bananas from my list

Claude: I'll remove bananas from your list.

[Tool: bring_remove_item]
- list_uuid: abc123-def456-ghi789
- item_name: Bananas

Successfully removed 'Bananas' from list abc123-def456-ghi789
```

### Remove Multiple Items

```
You: Remove carrots and lettuce from my shopping list

Claude: I'll remove those items.

[Tool: bring_batch_update_items]
- operation: REMOVE
- items: Carrots, Lettuce

Successfully performed REMOVE operation on 2 item(s)
```

## Smart Shopping Workflows

### Weekly Meal Planning

```
You: I'm planning to make pasta carbonara, chicken stir-fry, and tacos this week. Add the ingredients to my list.

Claude: Great! Let me add the ingredients for those meals:

For Pasta Carbonara:
- Spaghetti
- Eggs
- Bacon
- Parmesan cheese
- Black pepper

For Chicken Stir-Fry:
- Chicken breast
- Soy sauce
- Bell peppers
- Broccoli
- Garlic
- Ginger

For Tacos:
- Ground beef
- Taco shells
- Lettuce
- Tomatoes
- Cheese
- Sour cream

[Tool: bring_batch_update_items with all ingredients]

Successfully added 18 items to your Weekly Groceries list!
```

### Smart Substitutions

```
You: I see you have regular milk on the list. Can you replace it with almond milk?

Claude: I'll remove regular milk and add almond milk instead.

[Tool: bring_remove_item - Milk]
[Tool: bring_add_item - Almond milk]

Done! I've replaced regular milk with almond milk on your list.
```

### Shopping Trip Review

```
You: I just got back from the store. I bought everything except the apples (they looked bad) and I forgot to get the bread.

Claude: Let me update your list. I'll:
1. Mark the purchased items as complete
2. Keep apples on the list (since you didn't buy them)
3. Keep bread on the list (since you forgot it)

[Tool: bring_batch_update_items]
- operation: COMPLETE
- items: [all items except apples and bread]

Updated! Apples and bread are still on your active list.
```

## Catalog and Information Queries

### Item Details

```
You: What information do you have about the Milk item in the catalog?

Claude: Let me get the details about Milk from the Bring! catalog.

[Tool: bring_get_item_details]
- item_ids: ["Milk"]

Item Details:

Item: Milk
  Translations: {"en": "Milk", "de": "Milch", "es": "Leche"}
  Image: /images/items/milk.png
```

### Browse Catalog

```
You: Show me some breakfast items from the Bring! catalog

Claude: Let me get the full catalog and show you breakfast-related items.

[Tool: bring_get_all_item_details]
- locale: en-US

Here are some breakfast items available:
- Milk
- Eggs
- Bread
- Cereal
- Orange juice
- Yogurt
- Butter
- Jam
- Coffee
- Tea
```

### User Account Info

```
You: What's my Bring! account information?

Claude: Let me get your account details.

[Tool: bring_get_user_info]

User Information:

Email: you@example.com
User UUID: user-abc-123
Name: Your Name
Photo Path: /images/users/abc123.jpg
```

## Advanced Use Cases

### List Management for Events

```
You: I'm hosting a dinner party for 8 people. Help me create a shopping list for appetizers, main course, and dessert.

Claude: Great! Let me help you plan. What type of cuisine would you like?

You: Italian

Claude: Perfect! Here's a shopping list for an Italian dinner party for 8:

Appetizers:
- Mozzarella cheese
- Tomatoes
- Basil
- Olive oil
- Balsamic vinegar
- Prosciutto

Main Course:
- Pasta (lasagna sheets)
- Ground beef (1.5kg)
- Tomato sauce
- Ricotta cheese
- Parmesan cheese
- Garlic
- Onions

Dessert:
- Ladyfinger cookies
- Mascarpone cheese
- Espresso
- Cocoa powder
- Eggs

[Tool: bring_batch_update_items - all items]

Added 21 items to your Party Shopping list!
```

### Dietary Preferences

```
You: I'm switching to a plant-based diet. Can you suggest alternatives for the dairy items on my list?

Claude: I'll help you find plant-based alternatives:

Current item -> Plant-based alternative
- Milk -> Oat milk or almond milk
- Cheese -> Vegan cheese
- Yogurt -> Coconut yogurt
- Butter -> Vegan butter

Would you like me to:
1. Remove the dairy items and add the alternatives?
2. Add the alternatives while keeping the dairy items?
3. Just add the alternatives?

You: Option 1 - replace them all

Claude: [Executes batch operations to remove dairy and add plant-based alternatives]

Done! Your list now has all plant-based alternatives.
```

### Inventory Management

```
You: I have chicken, rice, and carrots at home. What else do I need from my list to make a complete meal?

Claude: Based on what you have, let me check your list:

You have: Chicken, Rice, Carrots

From your list, you could grab:
- Onions
- Garlic
- Soy sauce
- Ginger

This would give you everything for a chicken fried rice!

Want me to mark just those items or help plan something else?
```

## Tips for Best Results

1. **Be specific with list names**: If you have multiple lists, mention the specific list name
2. **Use natural language**: Claude understands "add milk" and "put milk on my list" equally well
3. **Batch operations**: When adding/removing multiple items, mention them all at once for efficiency
4. **Include specifications**: Mention quantities, brands, or preferences when adding items
5. **Review before shopping**: Ask Claude to show your list before heading to the store

## Troubleshooting Examples

```
You: I can't see my lists

Claude: Let me check your connection to Bring!

[Tool: bring_get_lists]

If error: "I'm having trouble connecting. Let's verify:
1. Is your internet connection working?
2. Are your Bring! credentials correct?
3. Is the Bring! service accessible?"

If successful: Shows your lists
```

```
You: It's not adding items

Claude: Let me try adding a test item to see what's happening.

[Tool: bring_add_item with test item]

[Provides specific error message and troubleshooting steps based on the result]
```
