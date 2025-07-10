"""
Example API tests demonstrating API testing capabilities.
Uses JSONPlaceholder as a sample API for testing.
"""

import pytest
import allure
import requests

from framework.utils.helpers import APIHelper
from framework.utils.logger import get_logger


logger = get_logger(__name__)


@allure.epic("API Testing")
@allure.feature("JSONPlaceholder API")
class TestExampleAPI:
    """Example API test cases using JSONPlaceholder."""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        """API client fixture for JSONPlaceholder."""
        return APIHelper(base_url="https://jsonplaceholder.typicode.com")
    
    @allure.story("Posts API")
    @allure.title("Get all posts")
    @allure.description("Test retrieving all posts from the API")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_posts(self, api_client):
        """Test getting all posts."""
        with allure.step("Send GET request to /posts"):
            response = api_client.get("/posts")
        
        with allure.step("Verify response"):
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
            
            posts = response.json()
            assert isinstance(posts, list), "Response should be a list"
            assert len(posts) > 0, "Should return at least one post"
            
            # Verify post structure
            first_post = posts[0]
            required_fields = ["id", "title", "body", "userId"]
            for field in required_fields:
                assert field in first_post, f"Post should have '{field}' field"
            
            # Attach response to allure report
            allure.attach(
                response.text,
                name="API Response",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.story("Posts API")
    @allure.title("Get specific post")
    @allure.description("Test retrieving a specific post by ID")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_get_specific_post(self, api_client):
        """Test getting a specific post by ID."""
        post_id = 1
        
        with allure.step(f"Send GET request to /posts/{post_id}"):
            response = api_client.get(f"/posts/{post_id}")
        
        with allure.step("Verify response"):
            assert response.status_code == 200
            
            post = response.json()
            assert post["id"] == post_id, f"Post ID should be {post_id}"
            assert "title" in post, "Post should have title"
            assert "body" in post, "Post should have body"
            assert "userId" in post, "Post should have userId"
    
    @allure.story("Posts API")
    @allure.title("Create new post")
    @allure.description("Test creating a new post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_create_post(self, api_client):
        """Test creating a new post."""
        new_post = {
            "title": "Test Post",
            "body": "This is a test post created by automation",
            "userId": 1
        }
        
        with allure.step("Send POST request to create new post"):
            response = api_client.post("/posts", json=new_post)
        
        with allure.step("Verify response"):
            assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
            
            created_post = response.json()
            assert created_post["title"] == new_post["title"]
            assert created_post["body"] == new_post["body"]
            assert created_post["userId"] == new_post["userId"]
            assert "id" in created_post, "Created post should have an ID"
    
    @allure.story("Posts API")
    @allure.title("Update existing post")
    @allure.description("Test updating an existing post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_update_post(self, api_client):
        """Test updating an existing post."""
        post_id = 1
        updated_post = {
            "id": post_id,
            "title": "Updated Test Post",
            "body": "This post has been updated by automation",
            "userId": 1
        }
        
        with allure.step(f"Send PUT request to update post {post_id}"):
            response = api_client.put(f"/posts/{post_id}", json=updated_post)
        
        with allure.step("Verify response"):
            assert response.status_code == 200
            
            updated = response.json()
            assert updated["id"] == post_id
            assert updated["title"] == updated_post["title"]
            assert updated["body"] == updated_post["body"]
    
    @allure.story("Posts API")
    @allure.title("Delete post")
    @allure.description("Test deleting a post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_delete_post(self, api_client):
        """Test deleting a post."""
        post_id = 1
        
        with allure.step(f"Send DELETE request for post {post_id}"):
            response = api_client.delete(f"/posts/{post_id}")
        
        with allure.step("Verify response"):
            assert response.status_code == 200
    
    @allure.story("Users API")
    @allure.title("Get all users")
    @allure.description("Test retrieving all users from the API")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_get_all_users(self, api_client):
        """Test getting all users."""
        with allure.step("Send GET request to /users"):
            response = api_client.get("/users")
        
        with allure.step("Verify response"):
            assert response.status_code == 200
            
            users = response.json()
            assert isinstance(users, list), "Response should be a list"
            assert len(users) > 0, "Should return at least one user"
            
            # Verify user structure
            first_user = users[0]
            required_fields = ["id", "name", "username", "email"]
            for field in required_fields:
                assert field in first_user, f"User should have '{field}' field"
    
    @allure.story("Comments API")
    @allure.title("Get comments for post")
    @allure.description("Test retrieving comments for a specific post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_get_post_comments(self, api_client):
        """Test getting comments for a specific post."""
        post_id = 1
        
        with allure.step(f"Send GET request to /posts/{post_id}/comments"):
            response = api_client.get(f"/posts/{post_id}/comments")
        
        with allure.step("Verify response"):
            assert response.status_code == 200
            
            comments = response.json()
            assert isinstance(comments, list), "Response should be a list"
            
            if comments:  # If there are comments
                first_comment = comments[0]
                required_fields = ["id", "name", "email", "body", "postId"]
                for field in required_fields:
                    assert field in first_comment, f"Comment should have '{field}' field"
                
                # Verify all comments belong to the correct post
                for comment in comments:
                    assert comment["postId"] == post_id, \
                        f"Comment postId should be {post_id}, got {comment['postId']}"
    
    @pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
    @allure.story("Posts API")
    @allure.title("Get posts with different IDs")
    @allure.description("Test retrieving posts with various IDs")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    def test_get_posts_parametrized(self, api_client, post_id):
        """Test getting posts with different IDs."""
        with allure.step(f"Get post with ID {post_id}"):
            response = api_client.get(f"/posts/{post_id}")
        
        with allure.step("Verify response"):
            assert response.status_code == 200
            
            post = response.json()
            assert post["id"] == post_id
            assert len(post["title"]) > 0, "Post title should not be empty"
            assert len(post["body"]) > 0, "Post body should not be empty"
    
    @allure.story("Error Handling")
    @allure.title("Handle non-existent post")
    @allure.description("Test API response for non-existent post")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    def test_get_nonexistent_post(self, api_client):
        """Test getting a non-existent post."""
        non_existent_id = 999999
        
        with allure.step(f"Send GET request for non-existent post {non_existent_id}"):
            response = api_client.get(f"/posts/{non_existent_id}")
        
        with allure.step("Verify error response"):
            assert response.status_code == 404, f"Expected 404 for non-existent post, got {response.status_code}"
    
    @allure.story("Response Time")
    @allure.title("Verify API response time")
    @allure.description("Test that API responds within acceptable time limits")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    def test_api_response_time(self, api_client):
        """Test API response time."""
        import time
        
        with allure.step("Measure response time for /posts"):
            start_time = time.time()
            response = api_client.get("/posts")
            end_time = time.time()
            
            response_time = end_time - start_time
        
        with allure.step("Verify response time"):
            assert response.status_code == 200
            assert response_time < 5.0, f"API should respond within 5 seconds, took {response_time:.2f}s"
            
            # Attach response time to report
            allure.attach(
                f"{response_time:.3f} seconds",
                name="Response Time",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.story("Data Validation")
    @allure.title("Validate post data structure")
    @allure.description("Test that post data has correct structure and types")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_post_data_validation(self, api_client):
        """Test post data structure validation."""
        with allure.step("Get first post"):
            response = api_client.get("/posts/1")
            assert response.status_code == 200
            
            post = response.json()
        
        with allure.step("Validate data types"):
            assert isinstance(post["id"], int), "Post ID should be integer"
            assert isinstance(post["userId"], int), "User ID should be integer"
            assert isinstance(post["title"], str), "Title should be string"
            assert isinstance(post["body"], str), "Body should be string"
        
        with allure.step("Validate data constraints"):
            assert post["id"] > 0, "Post ID should be positive"
            assert post["userId"] > 0, "User ID should be positive"
            assert len(post["title"].strip()) > 0, "Title should not be empty"
            assert len(post["body"].strip()) > 0, "Body should not be empty"
