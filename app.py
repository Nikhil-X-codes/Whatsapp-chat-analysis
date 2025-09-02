import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

# Configure matplotlib for dark theme
plt.style.use('dark_background')
sns.set_theme(style="darkgrid")

st.sidebar.title("WhatsApp Chat Analyzer")

# Upload file and convert into readable dataframe format
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.pre(data)

    # Show data preview until analysis button is clicked
    st.title("📱 WhatsApp Chat Data Preview")
    st.info("Your chat has been loaded successfully! Select a user and click 'Show Analysis' to begin.")

    # Display basic info about the dataset
    col1, col2 = st.columns(2)

    with col1:
        unique_users = len(df['user'].unique()) - 1
        st.metric("Unique Users", unique_users)

    with col2:
        start_date = df['date'].min().strftime('%Y-%m-%d')
        end_date = df['date'].max().strftime('%Y-%m-%d')
        date_range = f"{start_date} → {end_date}"

    st.metric("Date Range", date_range)

    # User selection
    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()  # Sort alphabetically
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis For", user_list)

    # Analysis section - only shows after button click
if st.sidebar.button("Show Analysis"):

        # Get statistics
        num_messages, num_words, num_media_messages, num_links = helper.stats(
            selected_user, df)

        # Clear the preview and show analysis
        st.title(f"📊 Analysis Results for: {selected_user}")

        # Top Statistics with dark theme colors
        st.header("📈 Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", f"{num_messages:,}", delta=None)
        with col2:
            st.metric("Total Words", f"{num_words:,}", delta=None)
        with col3:
            st.metric("Media Shared", f"{num_media_messages:,}", delta=None)
        with col4:
            st.metric("Links Shared", f"{num_links:,}", delta=None)

        st.markdown("---")

        if selected_user == 'Overall':
            st.header("👑 Most Active Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                ax.set_title('Top Users by Message Count', color='white', fontsize=14, fontweight='bold')
                ax.set_xlabel('Users', color='white', fontweight='bold')
                ax.set_ylabel('Messages', color='white', fontweight='bold')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                plt.xticks(rotation=45, ha='right', color='white')
                ax.grid(True, alpha=0.2, color='white', axis='y')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
            st.markdown("---")

        # Word Cloud
        st.header("☁️ Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        if df_wc is None:
            st.info("Word cloud not available (no text or missing optional library).")
        else:
            fig, ax = plt.subplots(figsize=(18, 12), facecolor='none')
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(f'Most Frequent Words - {selected_user}', color='white', fontsize=18, fontweight='bold')
            st.pyplot(fig, use_container_width=True)
            plt.close()

        st.markdown("---")

        # Emoji Analysis
        st.header("😊 Emoji Analysis")
        emoji_df = helper.emojis(selected_user, df)

        if not emoji_df.empty:
            col1 = st.columns(1)[0]
            with col1:
                st.subheader("Top Emojis")
                emoji_df_sorted = emoji_df.sort_values('count', ascending=False)
                st.dataframe(emoji_df_sorted, use_container_width=True)

        else:
            st.info("No emojis found in the selected messages.")

        st.markdown("---")

        # Monthly Timeline
        st.header("📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        # Sort chronologically: by year, then real month order
        month_order_map = {m: i for i, m in enumerate(['January','February','March','April','May','June','July','August','September','October','November','December'], start=1)}
        timeline['month_order'] = timeline['month_name'].map(month_order_map)
        timeline_sorted = timeline.sort_values(['year', 'month_order'])

        fig, ax = plt.subplots(figsize=(14, 6), facecolor='none')
        ax.plot(
            timeline_sorted['time'], timeline_sorted['message'],
            color='#00D4AA', linewidth=3, marker='o', markersize=8, markerfacecolor='#FF6B6B'
        )
        ax.fill_between(
            timeline_sorted['time'], timeline_sorted['message'], alpha=0.3, color='#00D4AA')

        ax.set_xlabel('Month-Year', color='white', fontweight='bold')
        ax.set_ylabel('Number of Messages', color='white', fontweight='bold')
        ax.set_title(
            f'Monthly Message Activity - {selected_user}', color='white', fontweight='bold', pad=20)

        # Style for dark theme
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.2, color='white')

        plt.xticks(timeline_sorted['time'], rotation=45, ha='right', color='white')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Weekly Timeline
        st.header("📊 Weekly Timeline")
        weekline = helper.weekly_timeline(selected_user, df)

        # Sort days properly
        day_order = ['Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekline['day_order'] = weekline['day_name'].map(
            {day: i for i, day in enumerate(day_order)})
        weekline_sorted = weekline.sort_values('day_order')

        fig, ax = plt.subplots(figsize=(14, 6), facecolor='none')
        ax.plot(
            weekline_sorted['day_name'], weekline_sorted['message'],
            color='#4ECDC4', linewidth=3, marker='s', markersize=10, markerfacecolor='#FF6B6B'
        )
        ax.fill_between(
            weekline_sorted['day_name'], weekline_sorted['message'], alpha=0.3, color='#4ECDC4')

        ax.set_xlabel('Day of Week', color='white', fontweight='bold')
        ax.set_ylabel('Number of Messages', color='white', fontweight='bold')
        ax.set_title(
            f'Weekly Message Activity - {selected_user}', color='white', fontweight='bold', pad=20)

        # Style for dark theme
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.2, color='white')

        plt.xticks(rotation=45, ha='right', color='white')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Month Timeline
        st.header("🗓️ Monthly Activity Pattern")
        monthline = helper.month_map(selected_user, df)

        if monthline is not None and not monthline.empty:
            # Sort months properly
            month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                           'July', 'August', 'September', 'October', 'November', 'December']
            monthline['month_order'] = monthline['month_name'].map(
                {month: i for i, month in enumerate(month_order)})
            monthline_sorted = monthline.sort_values('month_order')

            fig, ax = plt.subplots(figsize=(14, 6), facecolor='none')
            bars = ax.bar(
                monthline_sorted['month_name'], monthline_sorted['message'],
                color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD',
                       '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8C471', '#82E0AA'][:len(monthline_sorted)]
            )

            ax.set_xlabel('Month', color='white', fontweight='bold')
            ax.set_ylabel('Number of Messages', color='white', fontweight='bold')
            ax.set_title(
                f'Monthly Message Distribution - {selected_user}', color='white', fontweight='bold', pad=20)

            # Style for dark theme
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height + max(monthline_sorted['message']) * 0.01,
                    f'{int(height)}', ha='center', va='bottom', color='blue', fontweight='bold'
                )

            plt.xticks(rotation=45, ha='right', color='white')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        else:
            st.warning("No monthly data available for this user.")

        # Weekly Activity Heatmap
        st.header("🔥 Weekly Activity Heatmap")
        user_heatmap = helper.day_map(selected_user, df)

        if user_heatmap is None or user_heatmap.empty:
            st.info('No heatmap data available for this user.')
        else:
            fig, ax = plt.subplots(figsize=(16, 10), facecolor='none')
            # Create heatmap with dark-friendly colors
            sns.heatmap(
                user_heatmap, annot=False, cmap='plasma',
                cbar_kws={'label': 'Number of Messages'},
                linewidths=0.5, ax=ax
            )

            ax.set_title(f'Weekly Activity Heatmap - {selected_user}',
                         color='white', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Hour of Day', color='white', fontweight='bold')
            ax.set_ylabel('Day of Week', color='white', fontweight='bold')

            # Style colorbar for dark theme
            cbar = ax.collections[0].colorbar
            cbar.ax.yaxis.label.set_color('white')
            cbar.ax.tick_params(colors='white')

            # Style ticks for dark theme
            ax.tick_params(colors='white')

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        st.success(
            "✅ Analysis complete! Try selecting a different user to compare results.")

else:
    st.title("📱 WhatsApp Chat Analyzer")
    st.info("Please upload a WhatsApp chat export file to begin analysis.")
    st.markdown("""
    ### How to export your WhatsApp chat:
    1. Open WhatsApp on your phone
    2. Go to the chat you want to analyze
    3. Tap on the chat name at the top
    4. Scroll down and tap 'Export Chat'
    5. Choose 'With Media'
    6. Save the .txt file and upload it here
    """)
