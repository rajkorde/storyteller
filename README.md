# Storyteller

An AI Agent that creates customized stories for students with special needs.

## Overview

Storyteller is designed to address the unique challenge faced by educators working with students with special needs: the lack of centralized curriculum or resources tailored to individual requirements. This AI-powered tool helps teachers create personalized stories that cater to the specific needs, interests, and learning styles of each student.

## Purpose

There is no one-size-fits-all approach when working with students with special needs - each student requires individualized attention and resources. Storytelling is a powerful educational tool that can help students with special needs learn, grow, and develop essential skills. This AI Agent empowers teachers to generate stories that are:

- Tailored to individual student needs
- Appropriate for specific learning disabilities
- Engaging and educational
- Customizable based on student interests and abilities

## Features

- **Personalized Story Generation**: Create stories customized for individual students
- **Special Needs Focus**: Designed specifically for students with learning disabilities
- **Teacher-Friendly Interface**: Easy-to-use tool for educators
- **Adaptive Content**: Stories that adjust to different learning styles and abilities
- **Educational Value**: Stories designed to support learning objectives

## Getting Started

### Installation

```bash
uv venv
source .venv/bin/activate
uv pip install .
```

### Usage

```bash
uv run cli.py
```

### API Server

An HTTP API is also available to programmatically create stories.

```bash
uvicorn src.api:app --reload
```

The API also serves a small web interface at `/` where you can enter story details.

### Docker

To run on platforms like Railway using Docker:

```bash
docker build -t storyteller .
docker run -p 8000:8000 storyteller
```

Then open `http://localhost:8000` to use the frontend.

## Target Audience

- **Special Education Teachers**: Primary users who create stories for their students
- **Parents**: Caregivers of children with special needs
- **Therapists**: Speech, occupational, and behavioral therapists
- **Educational Support Staff**: Anyone working with special needs students

## License

MIT License
