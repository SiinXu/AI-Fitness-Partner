import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../contexts/AuthContext';
import ApiConfig from '../components/ApiConfig';

const Settings = () => {
  const router = useRouter();
  const { token } = useAuth();

  useEffect(() => {
    if (!token) {
      router.push('/login');
    }
  }, [token, router]);

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="relative px-4 py-10 bg-white mx-8 md:mx-0 shadow rounded-3xl sm:p-10">
          <div className="max-w-md mx-auto">
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <h2 className="text-2xl font-bold mb-8">Settings</h2>
                <ApiConfig />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
