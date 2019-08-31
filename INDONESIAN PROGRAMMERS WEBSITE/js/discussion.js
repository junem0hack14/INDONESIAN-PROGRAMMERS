class Discussion{
    /**
     * This class contains attributes of discussions made by the "INDONESIAN PROGRAMMERS" WhatsApp group members.
     * */
    constructor(number: Number, title: string){
        this._number = number;
        this._title = title;
        this._posts = [];
    }

    get number(){
        return this._number;
    }

    set number(number: Number){
        this._number = number;
    }

    get title(){
        return this._title;
    }

    set title(title: string){
        this._title = title;
    }

    get posts(){
        return this._posts;
    }

    set posts(posts: Array<Post>){
        this._posts = posts;
    }

    addPost(post: Post){
        this._posts.push(post);
    }

    removePost(index: Number){
        if (0 <= index < this._posts.length){
            this._posts.pop(index);
            return true;
        }
        return false;
    }
}