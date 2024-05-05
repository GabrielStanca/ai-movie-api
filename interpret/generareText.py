import random
import re
def generate_movie_descriptions(movies, templates):
    descriptions = []
    for movie in movies:
        # Select a random template for each movie
        template = random.choice(templates)
        # Generate the description using the movie's data
        description = template.format(title=movie["title"], rating=movie["rating"])
        descriptions.append(description)
    return descriptions

def generate_movie_descriptions_without_rating(titles, templates_without_rating):
    descriptions = []
    for full_title in titles:
        # Regex to extract title and year from the movie title format "Title (Year)"
        match = re.match(r"(.+?) \((\d{4})\)$", full_title)
        if match:
            title, year = match.groups()
        else:
            title = full_title  # Use the full title if no year is found
            year = "recent"

        # Use a template that requires title and year only
        template = random.choice(templates_without_rating)
        description = template.format(title=title, year=year)

        descriptions.append(description)
    return descriptions


def format_genres(genre_list):
    """Helper function to format genre list into a readable string."""
    if len(genre_list) > 1:
        return ', '.join(genre_list[:-1]) + ' and ' + genre_list[-1]
    elif genre_list:
        return genre_list[0]
    else:
        return "various genres"


def generate_movie_descriptions_with_genre(recommendation_data,templates_movies_year_genres):
    """Generates movie descriptions based on provided titles, years, and genres."""
    descriptions = []
    print(type(recommendation_data))
    print(recommendation_data)

    for film in recommendation_data["filme"]:
        title, year = film.rsplit(' (', 1)
        year = year[:-1]  # Remove the closing parenthesis
        genres = format_genres(recommendation_data["genuri"])
        template = random.choice(templates_movies_year_genres)  # Randomly choose a template
        description = template.format(title=title, year=year, genres=genres)
        descriptions.append(description)

    return descriptions


def get_genre_description(genre):
    # Define a dictionary mapping each genre to its specific sentence template
    genre_templates = {
        "Horror": "Step into the chilling world of Horror, where suspense and surprise lurk around every corner, thrilling audiences with spine-tingling tales.",
        "Fantasy": "Immerse yourself in the whimsical and imaginative realm of Fantasy, where magic and myth breathe life into the most extraordinary adventures.",
        "Action": "Experience the exhilaration of Action, a genre that pulses with energy from high-octane chases and explosive battles.",
        "Mystery": "Delve into the intricate plots and complex characters that define Mystery, a genre that invites viewers to untangle puzzles alongside the protagonists.",
        "Comedy": "Enjoy the light-hearted and uplifting moments of Comedy, where humor emerges through witty dialogue, slapstick antics, and delightful absurdities.",
        "Drama": "Revisit the timeless struggles and triumphs of Drama, where deep emotional storytelling captures the essence of the human experience.",
        "Musical": "Get swept away by the grandeur and romance of Musical films, where song and dance weave seamlessly into the narrative fabric.",
        "Crime": "Discover the gritty and gripping world of Crime, a genre that delves into the dark corners of society and the complexities of justice.",
        "Film-Noir": "Admire the artistic and narrative depth of Film-Noir, with its stylish cinematography and morally ambiguous characters.",
        "Western": "Explore the vast landscapes and enduring spirit of the Western, a genre that chronicles the tales of America's rugged frontier.",
        "Thriller": "Feel the tension and thrill of Thriller, where suspense is masterfully crafted to keep viewers on the edge of their seats.",
        "War": "Witness the harrowing battles and personal stories of War films, which bring historical and fictional wars to vivid life.",
        "Sci-Fi": "Ponder the universe and beyond with Sci-Fi, a genre that expands horizons and explores the possible futures of humanity.",
        "Documentary": "Learn and reflect with Documentary films, which offer insightful perspectives on real-world issues and stories.",
        "Adventure": "Join the adventures in Adventure films, where heroes embark on journeys filled with danger, mystery, and excitement.",
        "Children's": "Celebrate Children's films, a genre dedicated to enchanting and educating young minds through fun and engaging narratives.",
        "IMAX": "Dive into the innovative and visually captivating experiences offered by IMAX films, which bring cinematic wonders to life with breathtaking clarity.",
        "Animation": "Relive classic tales and new stories alike in Animation, where creativity knows no bounds and every frame is a work of art.",
        "Romance": "Navigate the complex stories of love and relationships within Romance, a genre that explores the emotional rollercoaster of the heart."
    }

    # Return the corresponding template sentence for the genre or a default message if the genre is not recognized
    return genre_templates.get(genre, "Genre not recognized. Please try a different genre.")

def generate_top_movies_intro(n):
    templates = [
        "Dive into the best of cinema with our Top {n} picks, showcasing films that have captivated audiences and critics alike.",
        "Explore our curated selection of the Top {n} movies, each a masterpiece that stands out in the realm of film.",
        "Here are the Top {n} films that you can't afford to miss—a lineup that promises exceptional storytelling and unforgettable experiences.",
        "Don't miss out on these Top {n} cinematic gems, each chosen for their unique contributions to the art of filmmaking.",
        "Presenting the Top {n} must-watch movies that have set the benchmarks for excellence in the industry.",
        "Immerse yourself in our exclusive Top {n} list, where each film is a window into the heights of cinematic creativity.",
        "Join us as we count down the Top {n} movies of all time, celebrating the best in narrative creativity and cinematic prowess.",
        "Discover the pinnacle of film with our Top {n} list, featuring movies that redefine the boundaries of storytelling."
    ]
    template = random.choice(templates)
    return template.format(n=n)
