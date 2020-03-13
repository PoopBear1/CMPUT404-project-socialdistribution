import React from 'react';
import AuthorHeader from './components/AuthorHeader'
import axios from 'axios';
import cookie from 'react-cookies';
import { Input, List} from 'antd';
import {USERNAME_LIST} from "./utils/constants.js";

const {Search} = Input;

class SearchPage extends React.Component{

    state = {
        usernames : [],
        value : '',
        isloading : true
    }

    componentDidMount(){
        this.fetchUsernames();
    }

    fetchUsernames = () => {
        axios.get(USERNAME_LIST, { headers: { 'Authorization': 'Token ' + cookie.load('token') } })
        .then(response => {
            this.setState({
                usernames : response.data["usernames"]
            })        
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    updateSearch = (val) => {
        this.setState({
            value : val,
            isloading : false
        })
    }

    handleClick = (usr) => {
        console.log(usr)
        document.location.replace("/author/".concat(usr).concat("/posts"))
    }

    render() {
        let filterUsernames = this.state.usernames.filter(
            (username) => {
                return username.toLowerCase().indexOf(
                    this.state.value.toLowerCase()) !== -1;
            }
        );
        return (
            <div>
                <AuthorHeader/>
                <div style={{textAlign:"center",marginTop:"10px"}}>
                <Search
                    style={{width:"30%"}}
                    placeholder="Enter to search author"
                    enterButton="Search"
                    size="large"
                    onChange={() => this.setState({isloading : true})}
                    onSearch={value => this.updateSearch(value)}
                />
                </div>
                <div>
                    {!this.state.isloading ?
                 <List
                    style={{marginLeft:"34.9%",width:"30%"}}
                    size="small"
                    bordered
                    dataSource={filterUsernames.map((username) => {
                        return username;
                    })}
                    renderItem={item => 
                        <List.Item>
                            <List.Item.Meta
                                style={{width:"30%"}}
                                title={<a href={"/author/".concat(item).concat("/posts")}>{item}</a>}
                            />
                            </List.Item>
                    }
                /> : null}
                </div>
                
            </div>
        )

    }
}

export default SearchPage;