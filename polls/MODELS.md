# Poll Models Documentation

## Overview
The poll system consists of two models: `Poll` and `Choice`, designed to allow users to create polls with 2-4 opinion choices.

## Models

### Poll Model
Represents a poll question with associated metadata.

**Fields:**
- `question` (CharField): The poll question text (max 200 characters)
- `created_date` (DateTimeField): Auto-populated timestamp when poll is created
- `poll_code` (CharField): Unique 8-character code for sharing polls (auto-generated)
- `is_active` (BooleanField): Whether the poll is active or closed

**Key Features:**
- ✅ Auto-generates unique 8-character poll code (e.g., "A7X9K2LP")
- ✅ Validates that each poll has 2-4 choices
- ✅ Tracks total votes across all choices
- ✅ Provides results with percentages

**Methods:**
- `generate_poll_code()`: Creates a unique alphanumeric code
- `clean()`: Validates poll has 2-4 choices
- `get_total_votes()`: Returns total vote count
- `get_results()`: Returns list of choices with votes and percentages

---

### Choice Model
Represents individual options/opinions in a poll.

**Fields:**
- `poll` (ForeignKey): Reference to parent Poll
- `text` (CharField): The choice text (max 200 characters)
- `vote_count` (IntegerField): Number of votes for this choice (default 0)

**Constraints:**
- ✅ Each poll must have minimum 2 choices
- ✅ Each poll can have maximum 4 choices
- ✅ Choices are deleted when parent poll is deleted (CASCADE)

---

## Usage Example

### Creating a Poll via Django Shell
```python
from polls.models import Poll, Choice

# Create a poll
poll = Poll.objects.create(question="What's your favorite programming language?")

# Add choices (2-4 required)
Choice.objects.create(poll=poll, text="Python")
Choice.objects.create(poll=poll, text="JavaScript")
Choice.objects.create(poll=poll, text="Go")

# Get poll code
print(poll.poll_code)  # e.g., "A7X9K2LP"

# Get results
print(poll.get_results())
```

### Via Django Admin
The admin interface provides inline editing of choices when creating/editing polls:
- Automatically shows 2 empty choice fields
- Enforces minimum 2 choices
- Enforces maximum 4 choices
- Displays vote counts (read-only)
- Shows poll code (auto-generated)

---

## Admin Features
- **List View**: Shows question, poll code, creation date, active status, choice count, and total votes
- **Inline Editing**: Add/edit choices directly within the poll form
- **Filtering**: Filter by active status and creation date
- **Search**: Search by question or poll code
- **Read-Only Fields**: Poll code, created date, and vote counts

---

## Database Relationships
```
Poll (1) -----> (Many) Choice
   |
   |-- question
   |-- poll_code (unique)
   |-- created_date
   |-- is_active
   |
   └── choices (2-4)
        |-- text
        |-- vote_count
```

---

## Validation Rules
1. **Minimum Choices**: Each poll must have at least 2 choices
2. **Maximum Choices**: Each poll cannot exceed 4 choices
3. **Unique Poll Code**: Each poll gets a unique 8-character code
4. **Vote Count**: Only incremented through voting logic (read-only in admin)

---

## Next Steps
- Implement voting logic
- Create poll creation views
- Add poll results visualization
- Implement poll sharing via code
