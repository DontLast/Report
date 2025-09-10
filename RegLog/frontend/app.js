const { createApp, ref, onMounted } = Vue;

createApp({
    setup() {
        const formData = ref({
            full_name: '',
            username: '',
            email: '',
            password: ''
        });

        const loading = ref(false);
        const message = ref('');
        const messageType = ref('');
        const users = ref([]);

        const API_BASE = 'http://localhost:8000';

        const submitForm = async () => {
            loading.value = true;
            message.value = '';

            try {
                const response = await fetch(`${API_BASE}/register/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData.value)
                });

                if (response.ok) {
                    const data = await response.json();
                    message.value = 'Регистрация успешна!';
                    messageType.value = 'success';

                    // Очищаем форму
                    formData.value = {
                        full_name: '',
                        username: '',
                        email: '',
                        password: ''
                    };

                    // Обновляем список пользователей
                    await loadUsers();
                } else {
                    const errorData = await response.json();
                    message.value = errorData.detail || 'Ошибка регистрации';
                    messageType.value = 'error';
                }
            } catch (error) {
                message.value = 'Ошибка соединения с сервером';
                messageType.value = 'error';
            } finally {
                loading.value = false;
            }
        };

        const loadUsers = async () => {
            try {
                const response = await fetch(`${API_BASE}/users/`);
                if (response.ok) {
                    users.value = await response.json();
                }
            } catch (error) {
                console.error('Ошибка загрузки пользователей:', error);
            }
        };

        onMounted(() => {
            loadUsers();
        });

        return {
            formData,
            loading,
            message,
            messageType,
            users,
            submitForm
        };
    }
}).mount('#app');