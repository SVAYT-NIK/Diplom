import { ConfigProvider, Layout, Typography, Spin } from 'antd'
import { QueryClient, QueryClientProvider } from 'react-query'
import ruRU from 'antd/locale/ru_RU'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'

dayjs.locale('ru')

const { Header, Content, Footer } = Layout
const { Title } = Typography

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider locale={ruRU}>
        <Layout style={{ minHeight: '100vh' }}>
          <Header style={{ display: 'flex', alignItems: 'center' }}>
            <Title level={3} style={{ color: 'white', margin: 0 }}>
              АСКУТЭ - Мониторинг энергоэффективности МКД
            </Title>
          </Header>
          <Content style={{ padding: '24px' }}>
            <div style={{ background: '#fff', padding: 24, minHeight: 360 }}>
              <Title level={4}>Добро пожаловать</Title>
              <p>
                Система мониторинга и анализа энергопотребления многоквартирных домов.
              </p>
              <Spin tip="Загрузка данных..." />
            </div>
          </Content>
          <Footer style={{ textAlign: 'center' }}>
            АСКУТЭ ©{new Date().getFullYear()} Created with React + TypeScript + Ant Design
          </Footer>
        </Layout>
      </ConfigProvider>
    </QueryClientProvider>
  )
}

export default App
