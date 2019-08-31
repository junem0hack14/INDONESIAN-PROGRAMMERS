class Post{
    /**
     * This class contains attributes of posts to be added to a discussion.
     * */

    constructor(posterName: string, contents: string){
        this._posterName = posterName;
        this._contents = contents;
    }

    get posterName(){
        return this._posterName;
    }

    set posterName(posterName: string){
        this._posterName = posterName;
    }

    get contents(){
        return this._contents;
    }

    set contents(contents: string){
        this._contents = contents;
    }
}