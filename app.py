import streamlit as st
import preprocessor,helper
import  matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyser")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data =bytes_data.decode("utf-8")
    #st.text(data)
    df=preprocessor.preprocess(data)
    #st.dataframe(df)

    # fetch unique user
    user_list=df['users'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert( 0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):

        num_messages , words , num_media,links=helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4= st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        with col4:
            st.header("Total Links")
            st.title(links)
        #monthly timeline
        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'] , color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #activity map

        st.title("Activity Map")
        col1, col2= st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_timeline(selected_user,df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index,busy_day.values)

            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.busy_month_timeline(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_month.index, busy_month.values , color='orange')
            st.pyplot(fig)

        #Most active users
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x,busy_df=helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1 , col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(busy_df)
        else:
            pass

    #WordCloud
        st.header('Wordcloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
    #MostCommonWords

        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

    #emojis
        st.title('Emoji analysis')
        emoji_df = helper.emoji_helper(selected_user,df)
        st.dataframe(emoji_df)














