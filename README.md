# 🚀 Startup Mentor

A powerful AI-powered startup mentoring application that provides comprehensive support for entrepreneurs through intelligent chat, business tools, and analytics.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-00A67E)](https://python.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT4-412991)](https://openai.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0.0-150458)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18.0-3F4F75)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🌟 Features

### 💬 Intelligent Chat Interface
- Real-time AI-powered responses to startup-related queries
- Context-aware conversations with source citations
- Multi-language support (English and German)
- Token usage tracking and cost monitoring

### 🛠️ Business Tools
- **Business Model Canvas Generator**
  - Problem statement analysis
  - Solution mapping
  - Target group identification
  - Comprehensive business model visualization

- **Pitch Deck Generator**
  - Structured pitch deck creation
  - Key message formulation
  - Professional presentation structure
  - Investor-ready content generation

### 📊 Analytics Dashboard
- Real-time token usage tracking
- Cost monitoring and analysis
- Usage patterns visualization
- Performance metrics

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- OpenAI API key
- Internet connection

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/startup-mentor.git
cd startup-mentor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## 🏗️ Architecture

The application is built using a modular architecture:

- **app.py**: Main application entry point
- **chat_manager.py**: Handles chat functionality and message history
- **tools_manager.py**: Manages business tools and their execution
- **dashboard.py**: Handles analytics and visualization
- **token_tracker.py**: Tracks and manages token usage
- **translations.py**: Manages multi-language support
- **help_guide.py**: Provides user guidance and documentation

## 🔧 Configuration

The application can be configured through environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `MODEL_NAME`: The OpenAI model to use (default: gpt-4)
- `TEMPERATURE`: Model temperature setting (default: 0.7)

## 🌐 Multi-language Support

The application currently supports:
- English (en)
- German (de)

Language can be changed through the sidebar selector.

## 📈 Token Usage Tracking

The application includes a comprehensive token tracking system:
- Real-time token counting
- Cost calculation
- Usage history
- Daily and total statistics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- Streamlit for the web framework
- LangChain for the AI framework
- All contributors and users of the application

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

Made with ❤️ for entrepreneurs and startup enthusiasts 