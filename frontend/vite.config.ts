import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
  proxy: {
    '/api': {
      target: 'https://case-df.local:8443',
      changeOrigin: true,
      secure: false, // don't reject self-signed/mkcert certs
    },
  },
},
  build: {
    outDir: '../backend/app/static',
    emptyOutDir: true,
  },
})

