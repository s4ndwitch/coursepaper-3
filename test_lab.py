
from serialiser.user import User
from serialiser.post import Post

def test_init_post():
    
    post = Post(uid = "asdf", signature="hello", author="qwerty", text="world")
    assert post.uid == "asdf"
    assert post.signature == "hello"
    assert post.author == "qwerty"
    assert post.text == "world"


def test_init_user():
    
    user = User(uid = "asdf", nickname="qwerty", pubkey="hello")
    assert user.uid == "asdf"
    assert user.nickname == "qwerty"
    assert user.pubkey == "hello"


from serialiser import Serialiser

serialiser: Serialiser
serialiser_post: Post
serialiser_user: User

def test_serialiser_create_user():
    
    global serialiser
    global serialiser_user
    
    serialiser = Serialiser(db_file="test.sqlite")
    
    serialiser_user = serialiser.createUser("qwerty", "wow")
    
    assert serialiser_user.nickname == "qwerty"
    assert serialiser_user.pubkey == "wow"

def test_serialiser_create_post():
    
    global serialiser
    global serialiser_post
    global serialiser_user
    
    serialiser_post = serialiser.createPost(serialiser_user.uid, "hello", "wow")
    
    assert serialiser_post.author == serialiser_user.uid
    assert serialiser_post.signature == "wow"
    assert serialiser_post.text == "hello"

def test_serialiser_get_post():
    
    global serialiser
    global serialiser_post
    
    get_post: Post = serialiser.getPost(serialiser_post.uid)
    
    assert get_post.uid == serialiser_post.uid
    assert get_post.author == serialiser_post.author
    assert get_post.signature == serialiser_post.signature
    assert get_post.text == serialiser_post.text

def test_serialiser_get_user():
    
    global serialiser
    global serialiser_user

    get_user: User = serialiser.getUser(serialiser_user.uid)
    
    assert get_user.uid == serialiser_user.uid
    assert get_user.nickname == serialiser_user.nickname
    assert get_user.pubkey == serialiser_user.pubkey

def test_serialiser_get_posts():
    
    global serialiser
    global serialiser_user
    global serialiser_post
    
    got_posts = serialiser.getPosts(serialiser_user.uid)
    
    assert got_posts == [ serialiser_post.uid ]

def test_serialiser_check_post_author():
    
    global serialiser_user
    global serialiser_post
    
    assert serialiser_post.author == serialiser_user.uid

from eqengine import EqEngine
import json

eqengine_first: EqEngine
eqengine_second: EqEngine

def test_eqengine_check_hello():

    global eqengine_first
    global eqengine_second
    
    eqengine_first = EqEngine("asdf", "127.0.0.1", 8080, "test_first.sqlite", "peer_first.ini")
    eqengine_second = EqEngine("qwer", "127.0.0.1", 8081, "test_second.sqlite", "peer_second.ini")
    
    eqengine_first.hello("127.0.0.1", 8081)
    eqengine_second.hello("127.0.0.1", 8080)
    
    peers_data_first = json.loads(open("peer_first.ini", "r").read())
    assert "qwer" in peers_data_first
    peers_data_second = json.loads(open("peer_second.ini", "r").read())
    assert "asdf" in peers_data_second

def test_eqengine_check_handle_data():
    
    global eqengine_first
    global eqengine_second
    
    eqengine_first.handleData(
        [{
            "type": "user",
            "uid": "asdf",
            "nickname": "asdf",
            "pubkey": "no"
        }], debug=True
    )
    
    eqengine_first.handleData(
        [{
            "type": "post",
            "uid": "post_uid_asdf",
            "author": "asdf",
            "text": "hello from asdf",
            "signature": "no"
        }], debug=True
    )

    post_first: Post = eqengine_first._serialiser.getPost("post_uid_asdf")
    
    assert post_first.uid == "post_uid_asdf"
    assert post_first.author == "asdf"
    assert post_first.text == "hello from asdf"
    assert post_first.signature == "no"

def test_eqengine_check_request():
    
    global eqengine_first
    
    post_first: dict = eqengine_first.request(
        [{
            "type": "post",
            "uid": "post_uid_asdf"
        }], online=False
    )[0]
    
    assert post_first["uid"] == "post_uid_asdf"
    assert post_first["author"] == "asdf"
    assert post_first["text"] == "hello from asdf"
    assert post_first["signature"] == "no"

from interface import Interface

interface_first = Interface("127.0.0.1", 8082, nickname="asdf",
                            db_file="asdf.sqlite", peer_file="asdf.ini", local_file="asdf_user.ini")
interface_second = Interface("127.0.0.1", 8083, nickname="qwer",
                             db_file="qwer.sqlite", peer_file="qwer.ini", local_file="qwer_user.ini")

interface_first.hello("127.0.0.1", 8083)
interface_second.hello("127.0.0.1", 8082)

def test_interface_check_post_write():
    
    global interface_first
    
    interface_first.writePost("hello from asdf")
    post: dict = interface_first.getPosts(interface_first._local_user.getUid())[0]
    
    assert post["text"] == "hello from asdf"
    assert post["author"] == interface_first._local_user.getUid()

def test_interface_check_follows():
    
    global interface_first
    global interface_second
    
    interface_second.follow(interface_first._local_user.getUid())
    
    assert interface_second.getFollows()[0] == interface_first._local_user.getUid()

def test_interface_check_internet_access():
    
    global interface_first
    global interface_second
    
    post: dict = interface_second.getPosts(interface_first._local_user.getUid())[0]
    
    assert post["author"] == interface_first._local_user.getUid()
    assert post["text"] == "hello from asdf"

import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def run_after_all_tests(request):
    def teardown():
        
        global eqengine_first
        global eqengine_second
        
        eqengine_first.shutdown()
        eqengine_second.shutdown()
        
        global interface_first
        global interface_second
        
        interface_first.shutdown()
        interface_second.shutdown()
        
        if os.path.exists("test.sqlite"):
            os.remove("test.sqlite")

        if os.path.exists("test_first.sqlite"):
            os.remove("test_first.sqlite")
        if os.path.exists("test_second.sqlite"):
            os.remove("test_second.sqlite")

        if os.path.exists("peer_first.ini"):
            os.remove("peer_first.ini")
        if os.path.exists("peer_second.ini"):
            os.remove("peer_second.ini")
            
        if os.path.exists("asdf.sqlite"):
            os.remove("asdf.sqlite")
        if os.path.exists("asdf.ini"):
            os.remove("asdf.ini")
        if os.path.exists("asdf_user.ini"):
            os.remove("asdf_user.ini")

        if os.path.exists("qwer.sqlite"):
            os.remove("qwer.sqlite")
        if os.path.exists("qwer.ini"):
            os.remove("qwer.ini")
        if os.path.exists("qwer_user.ini"):
            os.remove("qwer_user.ini")
    
    request.addfinalizer(teardown)
